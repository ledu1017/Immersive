// 캔버스 요소와 2D 컨텍스트 가져오기
const canvas = document.getElementById("ball-canvas");
const context = canvas.getContext("2d");

// 캔버스 중심 계산
const centerX = canvas.width / 2;
const centerY = canvas.height / 2;

// 6각형의 꼭지점 좌표 계산
const sides = 6; // 6각형
const radius = 100;
const vertexCoordinates = [];
for (let i = 0; i < sides; i++) {
    const angle = (Math.PI * 2 * i) / sides;
    const x = centerX + radius * Math.cos(angle);
    const y = centerY + radius * Math.sin(angle);
    vertexCoordinates.push({ x, y });
}

// 현재 공의 상태 (이동 중 또는 대기 중)
let ballState = "waiting";

// 공 초기 위치 설정 (중심으로)
let ballX = centerX;
let ballY = centerY;

// 현재 목표 꼭지점 인덱스와 이동 속도 설정
let targetVertexIndex = 0;
const speed = 2;

// 애니메이션 프레임 시작
ballState = "moving"; // 초기에 공을 이동 상태로 설정
animate();

function animate() {
    // 이전 프레임 지우기
    context.clearRect(0, 0, canvas.width, canvas.height);

    // 6각형 그리기
    context.beginPath();
    for (let i = 0; i < sides; i++) {
        context.lineTo(vertexCoordinates[i].x, vertexCoordinates[i].y);
    }
    context.closePath();
    context.stroke();

    if (ballState === "moving") {
        // 공 이동 및 그리기
        const targetX = vertexCoordinates[targetVertexIndex].x;
        const targetY = vertexCoordinates[targetVertexIndex].y;
        context.beginPath();
        context.arc(ballX, ballY, 10, 0, Math.PI * 2);
        context.fill();

        // 공을 다음 위치로 이동
        const dx = targetX - ballX;
        const dy = targetY - ballY;
        const distance = Math.sqrt(dx * dx + dy * dy);
        if (distance > speed) {
            ballX += (dx / distance) * speed;
            ballY += (dy / distance) * speed;
        } else {
            // 목표 꼭지점에 도달했을 때 다음 목표 꼭지점으로 변경
            targetVertexIndex = (targetVertexIndex + 1) % sides;

            // 공 상태 변경 (이동 중에서 대기 중으로)
            ballState = "waiting";

            // 일정 시간 후에 새로운 공을 중앙에서 랜덤한 꼭지점으로 보내기
            setTimeout(() => {
                const randomVertexIndex = Math.floor(Math.random() * sides);
                ballX = centerX;
                ballY = centerY;
                targetVertexIndex = randomVertexIndex;
                ballState = "moving";
            }, 1000); // 1000 밀리초 (1초) 후에 새로운 공 시작
        }
    } else if (ballState === "waiting") {
        // 대기 중인 공 그리기
        context.beginPath();
        context.arc(ballX, ballY, 10, 0, Math.PI * 2);
        context.fill();
    }

    // 애니메이션 프레임 요청
    requestAnimationFrame(animate);
}
