const { DataTypes } = requires('sequilize');
const { sequelize } = require('../config/db')
const Category = require('./Category')

const Product = sequelize.define('Product', {
    name: { type: DataTypes.STRING, allowNull: false},
    slug: { type:DataTypes.STRING , allowNull:false},
    description: { type:DataTypes.TEXT},
    price: { type: DataTypes.DECIMAL(10, 2), allowNull: false},
    stock: { type :DataTypes.INTEGER , allowNull:false , defaultValue: 0},
    image: { type: DataTypes.STRING}
}, {
    timestamps: true,
    tableName: 'products',
})

Product.belongsTo(Category, {foreignKey: 'categoryId', onDelete: 'CASCADE'}),
Category.hasMany(Product, { foreignKey: 'categoryId' });

module.exports = Product;