# goodside-amplify-mobile

<img src="https://rbcgithub.fg.rbc.com/AIH0/amp2021-team4/blob/master/images/Screen%20Shot%202021-08-05%20at%201.00.16%20PM.png" width="800"/>

## Frontend Tech Stack
- **React 16.13.1** - frontend JavaScript library 
- **React Native 0.63.3** - mobile application framework 
- **JavaScript** - frontend language 
- **React Navigation 4.3.9** - routing and navigation for your React Native apps 
- **UI Kitten 5.0.0** - UI component library
- **React Native Camera** - camera component

## Mobile Codebase Core Structure
This is the core src structure of the mobile codebase:
```
├── android
├── ios
├── node_modules
├── App.js
├── src
│   ├── components
│   │  ├── camera
│   │  ├── home
│   │  ├── insights
│   ├── navigations
│   ├── index.js
├── app.json
├── babel.config.js
├── index.js
├── metro.config.js
├── package.json
└── yarn.lock
```

## Getting Started React Native Mobile App
1. Clone the React Native Mobile App @ https://rbcgithub.fg.rbc.com/AIH0/goodside-amplify-mobile <br/>
2. CD into the root level, and run `npm i` <br/>
3. CD into `ios`, and run `pod install`, you may need to `setproxy` prior to this step to get it working <br/>
4. CD out into the root level, and run `npx react-native run-ios` <br/> <br/>
