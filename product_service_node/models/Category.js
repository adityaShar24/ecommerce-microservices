const { Datatype } = require('sequelize')
const { sequelize } = require('..config/db')

const Category = sequelize.define('Category', {
  name: { type: DataTypes.STRING, allowNull: false, unique: true },
  slug: { type: DataTypes.STRING, allowNull: false, unique: true },
  description: { type: DataTypes.TEXT, allowNull: true },
}, { timestamps: true });

module.exports = Category;