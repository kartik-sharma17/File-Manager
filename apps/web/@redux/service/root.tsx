import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'

export const RootApiService = createApi({
    reducerPath: 'rootApi',
    baseQuery: fetchBaseQuery({
        baseUrl: process.env.NEXT_PUBLIC_BASE_URL,
        prepareHeaders: (headers) => {
            if (typeof window !== 'undefined') {
                const token = localStorage.getItem('access_token')
                if (token) {
                    headers.set("Authorization", `Bearer ${token}`)
                }
            }
            return headers
        }
    }),
    tagTypes: ["Document"],
    endpoints: (build) => ({}),
})