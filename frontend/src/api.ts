const BASE_URL = 'http://127.0.0.1:8000'

export function saveTokenFromUrl(): void {
  const params = new URLSearchParams(window.location.search)
  const token = params.get('token')

  if (token) {
    localStorage.setItem('token', token)
  }
}

function getToken(): string {
  const token = localStorage.getItem('token')

  if (!token) {
    throw new Error('No token')
  }

  return token
}
export async function request<T>(options: {
  url: string
  method?: 'GET' | 'POST'
  body?: unknown
}): Promise<T> {
  const token = getToken()

  const res = await fetch(`${BASE_URL}${options.url}`, {
    method: options.method ?? 'POST',

    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },

    body: options.body
      ? JSON.stringify(options.body)
      : undefined,
  })
  return await res.json()
}
// export async function request<T>(options: {
//   url: string
//   method?: 'GET' | 'POST'
//   body?: unknown
// }): Promise<T> {
//   const token = localStorage.getItem('token')
//
//   const res = await fetch(`${BASE_URL}${options.url}`, {
//     method: options.method ?? 'POST',
//     headers: {
//       'Content-Type': 'application/json',
//       Authorization: `Bearer ${token}`,
//     },
//     body: options.body ? JSON.stringify(options.body) : undefined,
//   })
//
//   return await res.json()
// }