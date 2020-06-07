import React, { useState } from 'react';
import 'react-bootstrap-range-slider/dist/react-bootstrap-range-slider.css';
import RangeSlider from 'react-bootstrap-range-slider';

let tValue = -1;

const HelloWorld = (propesi) => {

  const [ value, setValue ] = useState(0);
  const [ status, setStatus ] = useState(false);


    let changeTime = setTimeout(() => {
        if (!status) {
            clearTimeout(changeTime);
            return;
        }
        clearTimeout(timerId);
        if (value < 1000) setValue(value + 1);
        else setValue(0);
    }, 1000);


    let timerId = setTimeout(() => {
        if(tValue != value) {
              let chtototam = fetch('/api/data', {
    method: 'POST',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({index: value})
  }).then((response) => {
    return response.json();
  })
  .then((data) => {
    propesi.updateData(data);
  });
            tValue = value;
        }

    }, 500);

  return (
    <div className={'fff'}>
        <img src={'https://image.flaticon.com/icons/svg/27/27185.svg'}  className={'zizhoba'} onClick={zizhobaPlay => {
            clearTimeout(timerId);
            clearTimeout(changeTime);
            setStatus(!status);
        }}></img>
        <RangeSlider
            max={1000}
          value={value}
          onChange={changeEvent => {
                  clearTimeout(timerId);
                  clearTimeout(changeTime);
                  if (status) setStatus(!status);
                  setValue(Number(changeEvent.target.value));
          }}
        />
        <div className={'danceTime'}>{((value * 30) - ((value * 30) % 60)) / 60 + ":" + (value * 30) % 60}</div>
    </div>
  );

};

export default HelloWorld