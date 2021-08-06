/**
 * Sample React Native App
 * https://github.com/facebook/react-native
 *
 * Generated with the UI Kitten goodsideamplifymobile
 * https://github.com/akveo/react-native-ui-kitten
 *
 * Documentation: https://akveo.github.io/react-native-ui-kitten/docs
 *
 * @format
 */

 import React from 'react';
 import { StyleSheet, TextInput, FlatList, View, ScrollView, Button, } from 'react-native';
 import { ApplicationProvider, Icon, IconRegistry, Layout, Text } from '@ui-kitten/components';
 import { EvaIconsPack } from '@ui-kitten/eva-icons';
 import * as eva from '@eva-design/eva';

// React Navigator
import 'react-native-gesture-handler';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';

// Insights import components
import { ScanInsights } from './src/components/grocery/insights/ScanInsights';
import { ScanInsightsNull } from './src/components/grocery/insights/ScanInsightsNull';
import { Insights } from './src/components/grocery/insights/Insight';
import { Company } from './src/components/grocery/insights/Company';
import { Transcation } from './src/components/grocery/insights/Transaction';
import { TranscationNull } from './src/components/grocery/insights/TranscationNull';
// Home import components
import { Scan } from './src/components/grocery/home/Scan'; 
import { ProductSearch } from './src/components/grocery/home/ProductSearch';
import { Trends } from './src/components/grocery/home/Trends';
import { Learn } from './src/components/grocery/home/Learn';
import { HomeScreen } from './src/components/grocery/home/HomeScreen';
import {InfoCard } from './src/components/grocery/InfoCards'
// Scan import components
import {ScanHistory} from './src/components/grocery/ScanHistoryScreen'
import { SuccessfulScan } from './src/components/grocery/SuccessfulScanScreen';
// Navigation import components
import { InsightsScreen } from './src/components/grocery/insights/InsightsScreen';
// Camera import components
import Camera from './src/components/grocery/camera/Camera'

// remove warning messages for demo
console.disableYellowBox = true; 

const HomeStack = createStackNavigator();

function App() {
  return (
    <ApplicationProvider {...eva} theme={eva.light}>
      <NavigationContainer>
        <HomeStack.Navigator>
          <HomeStack.Screen name="FoodPrint" component={HomeScreen} />
          <HomeStack.Screen name="Camera" component={Camera} />
          <HomeStack.Screen name="InfoCard" component={InfoCard} />
          <HomeStack.Screen name="Scan History" component={ScanHistory} />
          <HomeStack.Screen name="Successful Scan" component={SuccessfulScan} /> 
          <HomeStack.Screen name="Insights" component={InsightsScreen} />
        </HomeStack.Navigator>
        </NavigationContainer>
    </ApplicationProvider>
  )
}

export default App;