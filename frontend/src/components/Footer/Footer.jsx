import React from 'react'
import './footer.css'
import footer_logo from '../Assets/priceimg.png'
import outlook_logo from '../Assets/outlook.png'
import fb_logo from '../Assets/dv.png'
import insta_logo from '../Assets/instagram.png'
import whatsapp_logo from '../Assets/whatsapp.png'

export const Footer = () => {
return (
<div className='footer'>
    <div className="footerlogo">    <img src={footer_logo} alt="" />
    <p>Price Prediction</p>
    </div>
    <ul className="footerlink">
        <li>Company</li>
        <li>Predict</li>
        <li>About</li>
        <li>Contact</li>
    </ul>
    <div className="footer-gmail-icon">
    <div className="footericon_container">
            <img src={outlook_logo} alt="" />
        </div>
        <div className="footericon_container">
            <img src={fb_logo} alt="" />
        </div>
        <div className="footericon_container">
            <img src={insta_logo} alt="" />
        </div>
        <div className="footericon_container">
            <img src={whatsapp_logo} alt="" />
        </div>
    </div>
        
    <div className="footer-copyright">
        <hr/>    
        <p>Copyright @2023 - ALL Right Reserved        @Powered by CarNet.AI</p>
    </div>
</div>

  )
}

export default Footer
