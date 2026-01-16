import {Text, View, StyleSheet} from "react-native";

export default function Favorites(){
    return (
        <View style={styles.container}>
            <Text style={styles.text}>Favorites Page</Text>            
        </View>
    )
}

const styles = StyleSheet.create({
    container: {
        backgroundColor: "#ffffff",
        alignItems: "center",
        justifyContent: "center",
        flex: 1,
    },

    text: {
        color: "#754444",
    }

})