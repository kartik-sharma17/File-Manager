import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'

export const RootApiService = createApi({
    reducerPath: 'rootapi',
    baseQuery: fetchBaseQuery({ baseUrl: process.env.BASE_URL }),
    tagTypes: [],
    endpoints: () => ({}),
})