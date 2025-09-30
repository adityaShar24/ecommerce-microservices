const Category  = require('../models/Category');

exports.createCategory = async (req, res) => {
    try {
        const { name , slug , description} = req.body
        const category = await Category.create({name , slug , description})
        res.status(201).json(category)
    } catch (error) {
        console.error(error);
        res.status(500).json({error : 'Failed to create category'})
    }
}


exports.getCategoryById = async (req, res) => {
    try {
        const categories = await Category.findAll();
        res.status(200).json(categories)
    } catch (error) {
        res.status(500).json({error: 'Failed to fetch categories'})
    }
}
