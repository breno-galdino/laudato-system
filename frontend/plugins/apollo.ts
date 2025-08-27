import { ApolloClient, NormalizedCacheObject, from } from "@apollo/client/core";
import { provideApolloClient } from "@vue/apollo-composable";
import { removeTypenameFromVariables } from '@apollo/client/link/remove-typename';
import createUploadLink from "apollo-upload-client/createUploadLink.mjs";

interface Apollo {
  defaultClient: ApolloClient<NormalizedCacheObject>
  clients: ApolloClient<NormalizedCacheObject>[]
}

export default defineNuxtPlugin((nuxtApp) => {
  const runtimeConfig = useRuntimeConfig();

  const removeTypenameLink = removeTypenameFromVariables();


  const httpLink = createUploadLink({
    uri: runtimeConfig.public.apiUrl + "graphql",
    credentials: "include",
  })
  const client = (nuxtApp.$apollo as Apollo).defaultClient
  client.defaultOptions = {
    query: {
      fetchPolicy: "no-cache",
    },
  }
  client.setLink(from([removeTypenameLink, httpLink]))
  provideApolloClient(client)
});