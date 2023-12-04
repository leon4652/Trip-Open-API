const mysql = require('mysql');
const { MongoClient } = require('mongodb');

// MongoDB 연결 정보
const mongoUrl = 'mongodb+srv://S09P31B205:z5HxUpl4gB@ssafy.ngivl.mongodb.net/S09B31B205';
const fromCollectionName = 'summary_wiki_csv';
const toCollectionName = 'summary_overview';

// MySQL 연결 정보
const mysqlConfig = {
  host: 'k9b205.p.ssafy.io',
  user: 'b205',
  password: '9gi_ssafy_final',
  database: 'b205',
  charset: 'utf8',
};

const mysqlConnection = mysql.createConnection(mysqlConfig);

// 연결 및 실행 함수
const run = async () => {
  try {
    await mysqlConnection.connect();

    // MongoDB 연결
    const mongoClient = new MongoClient(mongoUrl, { useUnifiedTopology: true });
    await mongoClient.connect();

    const fromCollection = mongoClient.db().collection(fromCollectionName);
    const toCollection = mongoClient.db().collection(toCollectionName);

    // MongoDB에서 데이터 가져오기
    const pageList = await fromCollection.find({}).toArray();

    for (const page of pageList) {
      const contentId = page.content_id;

      // MySQL에서 데이터 가져오기
      const sql = `SELECT ad.overview FROM attraction_info as ai JOIN attraction_description as ad ON ai.content_id = ad.content_id WHERE ai.content_id = ${contentId}`;
      const [attractionArr] = await mysqlConnection.query(sql);

      let overview = 'null';
      if (attractionArr && attractionArr.length > 0 && attractionArr[0].overview) {
        overview = attractionArr[0].overview;
      }

      page.overview = overview;

      // MongoDB에 결과 저장
      await toCollection.updateOne({ _id: page._id }, { $set: { overview } });
    }

    console.log('데이터 마이그레이션 완료.');
  } catch (error) {
    console.error('에러:', error);
  } finally {
    await mysqlConnection.end();
    await mongoClient.close();
  }
};

run();
