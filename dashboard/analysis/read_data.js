// 필요한 라이브러리를 가져옵니다.
const XLSX = require('xlsx');

// 엑셀 파일의 경로를 지정합니다.
const excelFilePath = 'accident_data.xlsx'; // 실제 파일 경로로 변경하세요.

// 엑셀 파일을 읽어오는 함수를 정의합니다.
function readExcelFile(filePath) {
  try {
    const workbook = XLSX.readFile(filePath);
    const sheetName = workbook.SheetNames[0]; // 첫 번째 시트를 선택합니다.
    const sheet = workbook.Sheets[sheetName];
    
    // 엑셀 시트의 데이터를 JSON 형태로 파싱합니다.
    const jsonData = XLSX.utils.sheet_to_json(sheet, { header: 1 });
    
    return jsonData;
  } catch (error) {
    console.error('엑셀 파일을 읽어오는 중 오류가 발생했습니다:', error.message);
    return null;
  }
}

// 엑셀 파일을 읽어와서 데이터를 출력합니다.
const excelData = readExcelFile(excelFilePath);
if (excelData) {
  console.log('엑셀 데이터:');
  console.log(excelData);
}
