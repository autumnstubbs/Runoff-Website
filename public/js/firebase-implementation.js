// Import the functions you need from the SDKs you need
import { initializeApp } from "https://www.gstatic.com/firebasejs/9.2.0/firebase-app.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/9.2.0/firebase-analytics.js";
import { getDatabase, ref, child, get } from "https://www.gstatic.com/firebasejs/9.2.0/firebase-database.js";

// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration

// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyAtJmn6erCN842Rd6_JtO4-vGEz5vpmjDc",
  authDomain: "cisc475-498-eof-runoff-project.firebaseapp.com",
  projectId: "cisc475-498-eof-runoff-project",
  storageBucket: "cisc475-498-eof-runoff-project.appspot.com",
  messagingSenderId: "984037978789",
  appId: "1:984037978789:web:3cefc17cb8e735b88b934c",
  measurementId: "G-BNHJV3C11Q"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
const database = getDatabase(app);

const databaseRef = ref(database);
get(child(databaseRef, '0')).then((snapshot) => {
  if (snapshot.exists()) {
    console.log(snapshot.val());
  } else {
    console.log("No data available");
  }
}).catch((error) => {
  console.error(error);
});
