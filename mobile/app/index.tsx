import React, { useState } from 'react';
import { View, Text, Image, TextInput, TouchableOpacity, ActivityIndicator, StyleSheet, Alert } from "react-native";
import { ApiService } from "../services/api";

export default function Index() {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);

  const handleFetch = async () => {
    if (!url.includes('youtube.com') && !url.includes('youtu.be')) {
      Alert.alert("Invalid URL", "Please enter a valid YouTube link.");
      return;
    }

    setLoading(true);
    try {
      const recipe = await ApiService.getRecipe(url);
      console.log("Recipe Received:", recipe.title);
      Alert.alert("Recipe Found!", `Title: ${recipe.title}\nCalories: ${recipe.calories}`);
    } catch (error) {
      Alert.alert("Connection Error", "Check if your Flask server is running on the correct IP.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <View style={styles.container}>

      <Image 
        source={require('../assets/images/culinaire_logo.png')} 
        style={styles.logo} 
      />

      <Text style={styles.logo}>Culinaire</Text>
      
      <TextInput
        style={styles.input}
        placeholder="Paste YouTube Link"
        placeholderTextColor="#999"
        value={url}
        onChangeText={setUrl}
      />

      <TouchableOpacity 
        style={[styles.button, loading && { backgroundColor: '#444' }]} 
        onPress={handleFetch}
        disabled={loading}
      >
        {loading ? (
          <ActivityIndicator color="#fff" />
        ) : (
          <Text style={styles.buttonText}>Generate Recipe</Text>
        )}
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { 
    flex: 1,
    backgroundColor: "#ffffff", 
    alignItems: "center", 
    justifyContent: "center", 
    padding: 20 
  },

  logo: { 
    fontSize: 32, 
    fontWeight: 'bold',
    marginBottom: 40, 
    color: "#000" 
  },

  input: { 
    width: '100%',
    height: 50, 
    borderWidth: 1, 
    borderColor: "#ccc", 
    borderRadius: 10, 
    paddingHorizontal: 15, 
    marginBottom: 20 
  },

  button: { 
    width: '100%', 
    height: 50, 
    backgroundColor: 
    '#000', 
    borderRadius: 10, 
    justifyContent: 'center', 
    alignItems: 'center' 
  },

  buttonText: { 
    color: '#fff', 
    fontWeight: 'bold', 
    fontSize: 16 }
});