import {
  createDiscreteApi,
  darkTheme,
  lightTheme
} from "naive-ui";

const themeRef = ref("light");
const configProviderPropsRef = computed(() => ({
  theme: themeRef.value === "light" ? lightTheme : darkTheme
}));

const { message, notification, dialog, loadingBar } = createDiscreteApi(
  ["message", "dialog", "notification", "loadingBar"],
  {
    configProviderProps: configProviderPropsRef
  }
);

export  { message, notification, dialog, loadingBar }