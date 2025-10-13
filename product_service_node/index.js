const express = require('express')
const { connectDB, sequelize } = require('./config/db');
const Category = require('./models/Category');
const Product = require('./models/Product');

const app = express()
app.use(express.json())

connectDB()

sequelize.sync({ alter: true }).then(() => {
  console.log('Database synced!');
});

app.get('/', (req, res) => {
  res.json({ message: 'Product Service is running 🚀' });
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));