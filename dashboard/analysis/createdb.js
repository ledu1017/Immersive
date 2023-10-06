const firestoreService = require('firestore-export-import');
const firebaseConfig = require('./config.js')
const serviceAccount = require('school-db-account')

const jsonToFirestore = async() => {
    try{
        console.log('initialzing Firebase');
        await firestoreService.initializeFirebaseApp(serviceAccount, firebaseConfig.databaseURL);
        console.log('Firebase Initialized');

        await firestoreService.restore('./member.json');
        console.log('Upload success');
    }catch(error){
        console.log(error);
    }
};

jsonToFirestore();