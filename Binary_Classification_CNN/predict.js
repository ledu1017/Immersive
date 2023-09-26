let model;

async function loadModels() {
    model = await tf.loadLayersModel('model/model_json/model.json');
    console.log('Model loaded successfully');
}

async function predict(imageData) {
    if (!model) {
        console.error('Model is not loaded yet. Call loadModels() first.');
        return;
    }

    // 이미지 데이터를 모델에 입력
    const input = tf.browser.fromPixels(imageData).resizeBilinear([64, 64]).toFloat().div(255.0);
    const inputTensor = input.expandDims();

    const prediction = await model.predict(inputTensor).data();
    return prediction[0];
}

async function handleFileUpload(event) {
    const imageUpload = event.target;
    const result = document.getElementById('result');
    const uploadedImage = document.getElementById('uploadedImage'); // 이미지 요소

    if (!imageUpload.files || imageUpload.files.length === 0) {
        result.textContent = '이미지를 선택해주세요.';
        return;
    }

    const file = imageUpload.files[0];
    const image = new Image();
    image.src = URL.createObjectURL(file);

    image.onload = async () => {
        // 이미지가 로드되면 이미지 요소의 src 속성을 설정하여 이미지를 표시합니다.
        uploadedImage.src = image.src;

        const prediction = await predict(image);
        if (prediction >= 0.5) {
            result.textContent = '이 이미지는 폐렴(pneumonia)일 가능성이 있습니다.';
        } else {
            result.textContent = '이 이미지는 정상(normal)일 가능성이 있습니다.';
        }
    };
}

async function main() {
    await loadModels();

    const imageUpload = document.getElementById('imageUpload');
    imageUpload.addEventListener('change', handleFileUpload);
}

main();
