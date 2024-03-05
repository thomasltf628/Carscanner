import React from 'react';
import './hero.css';
import welcome_icon from '../Assets/welcome.png';
import arrow_icon from '../Assets/arrow.png';
import ai_icon from '../Assets/ai.png'
export const hero = () => {
  return (
    <div className='hero'>
        <div className="hero-left">
            <h2>Welcome To the SaveTheQueen</h2>
            <div>
                <div className="overiewicon">
                    <p>New</p>
                    <img src={welcome_icon} alt="" />
                </div>
                <p>Price Prediction</p>
                <p>FOR EVERYONE</p>
            </div>
            <div className="hero-latestbin">
                <div>Predict</div>
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