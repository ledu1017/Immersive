let model;

async function loadModels() {
    model = await tf.loadLayersModel('model/model.json');
    console.log('Model loaded successfully');
}

async function predict(temperature, humidity) {
    if (!model) {
        console.error('Model is not loaded yet. Call loadModel() first.');
        return;
    }

    const input = tf.tensor2d([[temperature, humidity]]);
    const prediction = await model.predict(input).data();
    return prediction[0];
}

async function handleFormSubmit(event) {
    event.preventDefault();

    const temperature = parseFloat(document.querySelector('#temperature').value);
    const humidity = parseFloat(document.querySelector('#humidity').value);

    if (isNaN(temperature) || isNaN(humidity)) {
        alert('온도와 습도를 유효한 숫자로 입력하세요.');
        return;
    }

    const prediction = await predict(temperature, humidity);

    const resultElement = document.querySelector('#predictionResult');
    resultElement.textContent = `예측 결과: ${prediction.toFixed(2)}`; // Display result with 2 decimal places
}

async function main() {
    await loadModels();

    const formElement = document.querySelector('#predictionForm');
    formElement.addEventListener('submit', handleFormSubmit);
}
// '현재 날씨' 버튼 클릭 이벤트 핸들러 추가
const getCurrentWeatherButton = document.querySelector('#getCurrentWeather');
getCurrentWeatherButton.addEventListener('click', () => {
    // API 호출 및 결과 표시
    getWeatherInfo();
});

// API 호출 및 결과 표시 함수 정의
async function getWeatherInfo() {
    const city = "Seoul";
    const apiKey = "0330caf4269a77dd6ac2332e5ac55c02";
    const lang = "kr";

    const apiUrl = `http://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${apiKey}&lang=${lang}&units=metric`;

    try {
        const response = await fetch(apiUrl);

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const weatherData = await response.json();
        const temperature = weatherData.main.temp;
        const humidity = weatherData.main.humidity;

        // 결과를 화면에 표시
        const weatherResultElement = document.querySelector('#weatherResult');
        weatherResultElement.innerHTML = `
            <p>현재 온도: ${temperature}°C</p>
            <p>현재 습도: ${humidity}%</p>
        `;
    } catch (error) {
        console.error(`Error: ${error.message}`);
    }
}

main();
