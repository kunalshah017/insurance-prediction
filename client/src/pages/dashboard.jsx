import React from "react";
import { PieChart, LineChart } from "@mui/x-charts";
import "tailwindcss/tailwind.css";
import AnimatedGradientText from "@/components/ui/animated-gradient-text";
import AnimatedGridPattern from "@/components/ui/animated-grid-pattern";
import Navbar from "@/components/navbar";
import { motion } from "framer-motion";

const fadeInUp = {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0 },
};

const Dashboard = () => {
    const recentTransactions = [
        { id: 1, date: "2024-12-20", description: "Grocery Shopping", category: "Groceries", status: "Completed", amount: -50.0 },
        { id: 2, date: "2024-12-18", description: "Electricity Bill", category: "Bills", status: "Completed", amount: -30.0 },
        { id: 3, date: "2024-12-15", description: "Salary", category: "Income", status: "Completed", amount: 500.0 },
        { id: 4, date: "2024-12-10", description: "Dining Out", category: "Dining", status: "Pending", amount: -20.0 },
        { id: 5, date: "2024-12-05", description: "Car Maintenance", category: "Auto", status: "Completed", amount: -120.0 },
        { id: 6, date: "2024-12-03", description: "Gym Membership", category: "Fitness", status: "Completed", amount: -50.0 },
        { id: 7, date: "2024-11-28", description: "Freelance Work", category: "Income", status: "Completed", amount: 300.0 },
    ];

    const expensesData = [
        { id: 0, label: "Groceries", value: 200 },
        { id: 1, label: "Bills", value: 150 },
        { id: 2, label: "Dining", value: 100 },
        { id: 3, label: "Entertainment", value: 50 },
        { id: 4, label: "Auto", value: 120 },
        { id: 5, label: "Fitness", value: 80 },
    ];

    const savingsData = [
        { x: "January", y: 500 },
        { x: "February", y: 700 },
        { x: "March", y: 600 },
        { x: "April", y: 800 },
        { x: "May", y: 1000 },
        { x: "June", y: 1100 },
        { x: "July", y: 1200 },
    ];

    const customerName = "Vinayak";

    return (
        <div className="bg-gray-50 min-h-screen">
            <AnimatedGridPattern />
            <div className="App relative z-10">
                <header className="App-header bg-white shadow-lg">
                    <Navbar />
                </header>

                <div className="p-8">
                    <motion.div
                        initial="hidden"
                        whileInView="visible"
                        viewport={{ once: true }}
                        variants={fadeInUp}
                        transition={{ duration: 1 }}
                    >
                        <AnimatedGradientText className="text-4xl font-extrabold mb-6">
                            Dashboard
                        </AnimatedGradientText>
                    </motion.div>
                    <p className="text-xl text-center text-gray-700 mb-8">Welcome to your dashboard, {customerName}!</p>

                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8 mb-12">
                        {[
                            { title: "Current Balance", amount: "$5,420.00", gradient: "from-blue-400 to-purple-500" },
                            { title: "Current Policy", amount: "Premium Savings Plan", gradient: "from-green-400 to-teal-500" },
                            { title: "Monthly Expenses", amount: "$1,230.00", gradient: "from-pink-400 to-red-500" },
                            { title: "Upcoming Payments", amount: "$200.00 (Due 2024-12-30)", gradient: "from-yellow-400 to-orange-500" },
                        ].map((card, index) => (
                            <motion.div
                                key={index}
                                className={`bg-gradient-to-r ${card.gradient} p-6 rounded-xl shadow-xl text-white hover:shadow-2xl transition-shadow`}
                                initial="hidden"
                                whileInView="visible"
                                viewport={{ once: true }}
                                variants={fadeInUp}
                                transition={{ duration: 1 }}
                            >
                                <h2 className="text-xl font-semibold">{card.title}</h2>
                                <p className="text-2xl font-bold mt-2">{card.amount}</p>
                            </motion.div>
                        ))}
                    </div>

                    <div className="grid grid-cols-1 lg:grid-cols-5 gap-8">
                        <motion.div
                            initial="hidden"
                            whileInView="visible"
                            viewport={{ once: true }}
                            variants={fadeInUp}
                            transition={{ duration: 1 }}
                            className="lg:col-span-3 bg-white p-6 rounded-xl shadow-xl"
                        >
                            <AnimatedGradientText className="text-xl font-semibold mb-4">Recent Transactions</AnimatedGradientText>
                            <table className="w-full table-auto text-left border-separate border-spacing-2">
                                <thead>
                                    <tr>
                                        <th className="py-2 px-4 bg-gray-100 rounded-lg">Date</th>
                                        <th className="py-2 px-4 bg-gray-100 rounded-lg">Description</th>
                                        <th className="py-2 px-4 bg-gray-100 rounded-lg">Category</th>
                                        <th className="py-2 px-4 bg-gray-100 rounded-lg">Status</th>
                                        <th className="py-2 px-4 bg-gray-100 rounded-lg">Amount</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {recentTransactions.map((transaction) => (
                                        <tr key={transaction.id}>
                                            <td className="py-2 px-4 border-b text-gray-600">{transaction.date}</td>
                                            <td className="py-2 px-4 border-b text-gray-700">{transaction.description}</td>
                                            <td className="py-2 px-4 border-b text-gray-700">{transaction.category}</td>
                                            <td className="py-2 px-4 border-b">
                                                <span
                                                    className={`px-2 py-1 rounded-full text-white ${transaction.status === "Completed"
                                                        ? "bg-green-500"
                                                        : "bg-yellow-500"
                                                        }`}
                                                >
                                                    {transaction.status}
                                                </span>
                                            </td>
                                            <td
                                                className={`py-2 px-4 border-b ${transaction.amount < 0 ? "text-red-600" : "text-green-600"
                                                    }`}
                                            >
                                                ${transaction.amount.toFixed(2)}
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </motion.div>

                        <motion.div
                            initial="hidden"
                            whileInView="visible"
                            viewport={{ once: true }}
                            variants={fadeInUp}
                            transition={{ duration: 1 }}
                            className="lg:col-span-2 grid grid-rows-2 gap-4"
                        >
                            <div className="bg-white p-6 rounded-xl shadow-xl flex flex-col items-center">
                                <AnimatedGradientText className="text-xl font-semibold mb-4 text-center">Expenses Breakdown</AnimatedGradientText>
                                <PieChart
                                    series={[{
                                        data: expensesData.map((item) => ({ id: item.id, value: item.value, label: item.label })),
                                        highlightScope: { fade: 'global', highlight: 'item' },
                                        faded: { innerRadius: 30, additionalRadius: -30, color: 'gray' },
                                    }]}
                                    height={220}
                                />
                            </div>
                            <div className="bg-white p-6 rounded-xl shadow-xl">
                                <AnimatedGradientText className="text-xl font-semibold mb-4 text-center">Savings Over Time</AnimatedGradientText>
                                <LineChart
                                    xAxis={[{ data: savingsData.map((item) => item.x), scaleType: "point" }]}
                                    series={[{
                                        data: savingsData.map((item) => item.y),
                                    }]}
                                    width={400}
                                    height={270}
                                />
                            </div>
                        </motion.div>
                    </div>

                    {/* About Us Section */}
                    <motion.section
                        id="about-bottom"
                        className="about-section bg-white shadow-lg rounded-lg p-8 my-12"
                        initial="hidden"
                        whileInView="visible"
                        viewport={{ once: true }}
                        variants={fadeInUp}
                        transition={{ duration: 1 }}
                    >
                        <AnimatedGradientText className="text-3xl font-bold text-center mb-6">
                            About Us
                        </AnimatedGradientText>
                        <motion.p
                            className="text-lg leading-relaxed text-center max-w-3xl mx-auto"
                            initial="hidden"
                            whileInView="visible"
                            viewport={{ once: true }}
                            variants={fadeInUp}
                            transition={{ duration: 1 }}
                        >
                            At AI Insurance Solutions, we merge technology and innovation to create insurance solutions
                            tailored to your needs. Explore our policies and discover how we can help secure your future.
                        </motion.p>
                    </motion.section>
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
