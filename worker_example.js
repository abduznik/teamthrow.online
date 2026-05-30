const CORS = {
  'Access-Control-Allow-Origin': 'https://teamthrow.online',
  'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
}

async function dispatch(eventType, payload, token) {
  const res = await fetch('https://api.github.com/repos/abduznik/teamthrow.online/dispatches', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Accept': 'application/vnd.github.v3+json',
      'Content-Type': 'application/json',
      'User-Agent': 'TeamThrow-Worker'
    },
    body: JSON.stringify({ event_type: eventType, client_payload: payload })
  })
  return res.status === 204
}

async function getYouTubeFeed(channelId) {
  const res = await fetch(`https://www.youtube.com/feeds/videos.xml?channel_id=${channelId}`, {
    headers: { 'User-Agent': 'TeamThrow-Worker' }
  })
  if (res.status !== 200) return { error: 'feed fetch failed', videos: [] }
  const text = await res.text()
  const videos = []
  const entryRe = /<entry>([\s\S]*?)<\/entry>/g
  let match
  while ((match = entryRe.exec(text)) !== null) {
    const e = match[1]
    const title = (e.match(/<title>(.*?)<\/title>/) || ['', ''])[1]
    const videoId = (e.match(/<yt:videoId>(.*?)<\/yt:videoId>/) || ['', ''])[1]
    const published = (e.match(/<published>(.*?)<\/published>/) || ['', ''])[1]
    const author = (e.match(/<name>(.*?)<\/name>/) || ['', ''])[1]
    if (videoId) videos.push({ title, videoId, published, author })
  }
  return { videos }
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url)

    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: CORS })
    }

    // GET endpoint: fetch YouTube channel RSS feed, return JSON
    if (request.method === 'GET' && url.pathname === '/youtube-feed') {
      const channelId = url.searchParams.get('channel_id') || 'UCyZesfM1i6yY5lSDG9v7UVg'
      const data = await getYouTubeFeed(channelId)
      return new Response(JSON.stringify(data), {
        status: data.error ? 502 : 200,
        headers: { ...CORS, 'Content-Type': 'application/json' }
      })
    }

    if (request.method !== 'POST') {
      return new Response('nope', { status: 405, headers: CORS })
    }

    const body = await request.json()
    let ok = false

    if (url.pathname === '/recruit') {
      ok = await dispatch('new_recruit', {
        battletag: body.battletag,
        hero: body.hero,
        winrate: body.winrate,
        story: body.story,
        timestamp: new Date().toISOString()
      }, env.GH_TOKEN)
    } else if (url.pathname === '/fanart') {
      ok = await dispatch('new_fanart', {
        artist: body.artist,
        title: body.title,
        imgur_url: body.imgur_url || body.image,
        artistLink: body.artistLink,
        description: body.description,
        timestamp: new Date().toISOString()
      }, env.GH_TOKEN)
    } else if (url.pathname === '/video') {
      ok = await dispatch('new_video', {
        title: body.title,
        uploader: body.uploader,
        url: body.url,
        timestamp: new Date().toISOString()
      }, env.GH_TOKEN)
    } else {
      return new Response('not found', { status: 404, headers: CORS })
    }

    return new Response(JSON.stringify({ ok }), {
      status: ok ? 200 : 500,
      headers: { ...CORS, 'Content-Type': 'application/json' }
    })
  }
}
