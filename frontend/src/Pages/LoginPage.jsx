import React from 'react'
import './Css/Loginpage.css'

export const LoginPage = () => {
  return (
    <div className='loginsignup'>
      <div className="loginsignup-contaier">
        <h1>Sign up</h1>
        <div className="loginsignup-field">
          <input type='text' placeholder='Your Name' />
          <input type='email' placeholder='Your Email' />
          <input type='password' placeholder='Password' />
        </div>
        <button>Continue</button>
        <p className='loginsignup-login'>Already have an account? <span>Login Here</span></p>
        <div className="loginsignup-agree">
          <input type='checkbox' name='' id='' />
          <p>By Continuing, I agree to the terms and privacy policy</p>
        </div>
      </div>
    </div>
  )
}
export default LoginPage