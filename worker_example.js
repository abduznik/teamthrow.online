const CORS = {
  'Access-Control-Allow-Origin': 'https://teamthrow.online',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
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

export default {
  async fetch(request, env) {

    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: CORS })
    }

    if (request.method !== 'POST') {
      return new Response('nope', { status: 405, headers: CORS })
    }

    const url = new URL(request.url)

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
