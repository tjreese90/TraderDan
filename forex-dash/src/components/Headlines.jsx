import React from 'react'
import TitleHead from './TitleHead'
import endPoints from '../app/api'
import { useState, useEffect } from 'react'
import Headline from './Headline'

function Headlines() {

const [headlines, setHeadlines] = useState(null)

useEffect(() => {
    loadAccount();
}, [])

const loadAccount = async () =>{
    const data = await(endPoints.headlines());
    setHeadlines(data);
}


  return (
    <div>
        
        <TitleHead title="Headlines" />
        <div className='segment'>
            {headlines && headlines.map((item, index) => {
                console.log(item)
                return <Headline key={index} data={item} />
            })}
        </div>
    </div>
  )
}

export default Headlines