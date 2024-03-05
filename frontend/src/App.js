import React, { useState, useEffect } from "react";
import './App.css'
import { Navbar } from "./components/Navbar/Navbar";
import {BrowserRouter,Routes,Route} from 'react-router-dom'

import { Result } from "./Pages/result";
import { About } from "./Pages/about";
import { Home } from "./Pages/home";
import { LoginPage } from "./Pages/LoginPage";

const App = () => {
  return (
    <div >
      <BrowserRouter>
      <Navbar/>
      <Routes>
        <Route path="/" element={<Home/>}></Route>
        <Route path="about" element={<About/>}></Route>
        <Route path="login" element={<LoginPage/>}></Route>
        <Route path="result" element={<Result/>}></Route>

      </Routes>
      </BrowserRouter>
    </div> 

  )
}
export default App