import { Stack } from "expo-router";
import * as SplashScreen from 'expo-splash-screen';
import { useFonts, BeauRivage_400Regular } from '@expo-google-fonts/beau-rivage';
import { useEffect } from 'react';

SplashScreen.preventAutoHideAsync();

export default function RootLayout() {
  const [loaded, error] = useFonts({
    'BeauRivage': BeauRivage_400Regular,
  });

  useEffect(() => {
    if (loaded || error) {
      SplashScreen.hideAsync();
    }
  }, [loaded, error]);

  if (!loaded && !error) {
    return null;
  }

  return (
    <Stack>
      <Stack.Screen name="index" options={{ headerShown: false }} />
      <Stack.Screen name="favorites" options={{ title: "Favorites" }} />
    </Stack>
  );
}