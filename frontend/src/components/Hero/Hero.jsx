import React from 'react';
import './hero.css';
import welcome_icon from '../Assets/welcome.png';
import arrow_icon from '../Assets/arrow.png';
import ai_icon from '../Assets/ai.png'
import {Link} from 'react-router-dom'

export const hero = () => {
  return (
    <div className='hero'>
        <div className="hero-left">
            <h2>Looking for car</h2>
            <div>
                <div className="overiewicon">
                    <p>Get</p>
                </div>
                <p>Your</p>
                <p>Best deal</p>
            </div>
            <div className="hero-latestbin">
                <div><Link style={{textDecoration: 'none'}} to='result'>Find your car</Link></div>
                <img src={arrow_icon} alt="" />
            </div>
        </div>
        <div className="hero-right">
        <img src={ai_icon} alt="" />
        </div>
    </div>
  )
}
export default hero