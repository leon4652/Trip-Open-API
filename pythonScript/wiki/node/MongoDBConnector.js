const { MongoClient } = require('mongodb');
const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

class MongoDBConnector {
  constructor(collection) {
    this.collectionName = collection;
    this.client = null;
    this.db = null;
    this.collection = null;
  }

  async connect() {
    try {
      this.client = new MongoClient('mongodb+srv://S09P31B205:z5HxUpl4gB@ssafy.ngivl.mongodb.net/S09B31B205', {
        useNewUrlParser: true,
        useUnifiedTopology: true,
      });
      await this.client.connect();
      this.db = this.client.db('S09P31B205');
      this.collection = this.db.collection(this.collectionName);
    } catch (error) {
      console.error('Failed to connect to MongoDB:', error);
    }
  }

  async insertData(data) {
    if (!this.collection) {
      await this.connect();
    }

    try {
      const result = await this.collection.insertOne(data);
      return result.insertedId;
    } catch (error) {
      console.error('Failed to insert data:', error);
      return null;
    }
  }

  async findData(data) {
    if (!this.collection) {
      await this.connect();
    }

    try {
      const result = await this.collection.findOne({ title: data });
      return result;
    } catch (error) {
      console.error('Failed to find data:', error);
      return null;
    }
  }

  async findAll() {
    if (!this.collection) {
      await this.connect();
    }

    try {
      const result = await this.collection.find({}).toArray();
      return result;
    } catch (error) {
      console.error('Failed to find all data:', error);
      return [];
    }
  }
}

// Example usage:
const connector = new MongoDBConnector('summary_overview');
(async () => {
  await connector.connect();
  const allData = await connector.findAll();
  console.log('All data:', allData);
})();
