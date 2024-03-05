import React, { useState } from "react";
import './Upload.css'
import axios from "axios";

import DataTable from "../DataTable/DataTable";

function Imageupload(){
    const [picture, setPicture] = useState('');
    const [jsonData, setJsonData] = useState(null);
    const [modelName, setModelName] = useState('');
    function handleImage(e){
      console.log(e.target.files)
      setPicture(e.target.files[0])
    }
    async function handleApi(){
      const formData = new FormData()
      formData.append('picture', picture)
      await axios.post('http://localhost:8000/api/n_profiles/', formData).then((res) => {
        console.log(res.data) 
        const extractedModel = res.data.model_name;
        setModelName(res.data.make_name + " " + res.data.model_name)
        return axios.get(`http://localhost:8000/api/cars/?model=${extractedModel}`);
      }).then(
        response => typeof response.data ==='string'? JSON.parse(response.data): response.data).then(data => { 
        setJsonData(data);
      }).catch((error) => console.error('Error fetching data:', error));
    }


    return(
      <div class = "image-upload-container">
        <input class = 'custom-file-upload' type="file" name='file' onChange ={handleImage}/>
        <p> </p>
        <button class = 'submit-button' onClick= {handleApi}>Submit</button>

        {modelName && <h3 class = "model-name">It is a {modelName}</h3>}
        <DataTable class="data-table" jsonData={jsonData}/>
      </div>

    
    )
}

export default Imageupload;
