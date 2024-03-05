import React, { useState } from 'react'
import './Navbar.css'
import logo from '../Assets/priceimg.png'
import iicon from '../Assets/letter.png'
import loginlogo from '../Assets/enter.png'
import {Link} from 'react-router-dom'

export const Navbar = () => {
  const [menu,setMenu]=useState("home")
  return (
    <div className='navbar'>
    <div className="nav-logo">
      <img src={logo} alt='' />
        <p>Price Prediction</p>
    </div>
    <ul className='nav-menu'>
        <li onClick={()=>{setMenu("home")}}><Link style={{textDecoration: 'none'}} to='/'>Home</Link>{menu==="home"?<hr/>:<></>}</li>
        <li onClick={()=>{setMenu("result")}}><Link style={{textDecoration: 'none'}} to='result'>Result</Link>{menu==="result"?<hr/>:<></>}</li>
        <li onClick={()=>{setMenu("about")}}><Link style={{textDecoration: 'none'}} to='about'>About</Link>{menu==="about"?<hr/>:<></>}</li>
      </ul>
      <div className='nav-login'>
      <Link to='login'><button>Login</button></Link>
        <img src={loginlogo} alt="" />
      </div>
</div>
  )
}
