import React, { useState, useEffect } from 'react';
import 'tailwindcss/tailwind.css';
import { motion } from 'framer-motion';
import AnimatedGradientText from '@/components/ui/animated-gradient-text';
import AnimatedGridPattern from '@/components/ui/animated-grid-pattern';
import Navbar from '@/components/navbar';

function Home() {
    const fadeInUp = {
        hidden: { opacity: 0, y: 50 },
        visible: { opacity: 1, y: 0 },
    };

    const [scrollPosition, setScrollPosition] = useState(0);
    const [maxScroll, setMaxScroll] = useState(0);

    useEffect(() => {
        const container = document.getElementById('policyContainer');
        const updateScroll = () => {
            setScrollPosition(container.scrollLeft);
            setMaxScroll(container.scrollWidth - container.clientWidth);
        };
        container.addEventListener('scroll', updateScroll);
        updateScroll();
        return () => container.removeEventListener('scroll', updateScroll);
    }, []);

    const handleScroll = (direction) => {
        const container = document.getElementById('policyContainer');
        if (direction === 'right') {
            container.scrollBy({ left: 300, behavior: 'smooth' });
        } else {
            container.scrollBy({ left: -300, behavior: 'smooth' });
        }
    };

    return (
        <div className="bg-gray-50 min-h-screen">
            <AnimatedGridPattern />

            <div className="App relative z-10">
                <header className="App-header bg-white shadow-lg">
                    <Navbar />
                </header>

                <main className="main-content container mx-auto py-12 px-6">
                    <motion.section
                        className="hero text-center py-16 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg shadow-lg"
                        initial="hidden"
                        animate="visible"
                        variants={fadeInUp}
                        transition={{ duration: 1 }}
                    >
                        <AnimatedGradientText className="text-6xl font-extrabold mb-6 drop-shadow-lg">
                            Welcome to AI Insurance Solutions
                        </AnimatedGradientText>
                        <p className="text-xl mb-8 max-w-2xl mx-auto leading-relaxed">
                            Revolutionizing insurance with AI-driven personalized recommendations and insights.
                        </p>
                        <motion.a
                            className="cta-button bg-white text-blue-600 py-3 px-6 rounded-lg shadow-md text-lg font-semibold hover:bg-gray-100 transition duration-200"
                            href="#policies"
                            whileHover={{ scale: 1.1 }}
                        >
                            Explore Our Policies
                        </motion.a>
                    </motion.section>

                    <section id="features" className="features-section bg-white shadow-lg rounded-lg p-8 my-12">
                        <AnimatedGradientText className="text-3xl font-bold text-center mb-6">
                            Features
                        </AnimatedGradientText>
                        <ul className="space-y-6">
                            {[
                                "Personalized insights to deepen understanding of customer behavior.",
                                "Optimized policy upselling with tailored pricing and durations.",
                                "Enhanced customer retention with AI-driven strategies."
                            ].map((feature, index) => (
                                <motion.li
                                    key={index}
                                    className="flex items-start"
                                    initial="hidden"
                                    whileInView="visible"
                                    viewport={{ once: true }}
                                    variants={fadeInUp}
                                    transition={{ duration: 0.8, delay: index * 0.2 }}
                                >
                                    <div className="bg-blue-600 text-white w-10 h-10 flex items-center justify-center rounded-full mr-6 text-lg font-semibold">
                                        {index + 1}
                                    </div>
                                    <p className="text-lg">{feature}</p>
                                </motion.li>
                            ))}
                        </ul>
                    </section>

                    <section id="policies" className="policies-section bg-white shadow-lg rounded-lg p-8 my-12 relative">
                        <AnimatedGradientText className="text-3xl font-bold text-center mb-6">
                            Policy Purchase
                        </AnimatedGradientText>
                        <motion.div
                            id="policyContainer"
                            className="overflow-hidden flex space-x-6"
                            initial="hidden"
                            whileInView="visible"
                            viewport={{ once: true }}
                            variants={{
                                hidden: { opacity: 0 },
                                visible: { opacity: 1, transition: { staggerChildren: 0.2 } },
                            }}
                        >
                            {[
                                "Life Insurance",
                                "Health Insurance",
                                "Travel Insurance",
                                "Term Plans",
                                "Pension Plans",
                                "Child Plans",
                                "Investment Plans",
                                "Critical Illness Coverage",
                                "ULIPs"
                            ].map((policy, index) => (
                                <motion.div
                                    key={index}
                                    className="policy-card bg-gradient-to-br from-blue-50 to-blue-100 shadow-lg rounded-lg p-6 w-64 flex-shrink-0 hover:shadow-2xl transition-shadow duration-200"
                                    variants={fadeInUp}
                                >
                                    <h3 className="text-xl font-bold mb-4 text-blue-600">{policy}</h3>
                                    <p className="text-sm mb-6 text-gray-600">
                                        Secure your future with our {policy.toLowerCase()} options.
                                    </p>
                                    <motion.button
                                        className="bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-500 transition duration-200"
                                        whileHover={{ scale: 1.05 }}
                                    >
                                        Learn More
                                    </motion.button>
                                </motion.div>
                            ))}
                        </motion.div>

                        {scrollPosition > 0 && (
                            <button
                                className="absolute left-4 top-1/2 transform -translate-y-1/2 bg-gradient-to-r from-purple-500 to-blue-600 text-white p-3 rounded-full shadow-lg hover:scale-110 transition"
                                onClick={() => handleScroll('left')}
                            >
                                <svg
                                xmlns="http://www.w3.org/2000/svg"
                                className="h-6 w-6"
                                fill="none"
                                viewBox="0 0 24 24"
                                stroke="currentColor"
                            >
                                <path
                                    strokeLinecap="round"
                                    strokeLinejoin="round"
                                    strokeWidth={2}
                                    d="M15 19l-7-7 7-7"
                                />
                            </svg>
                            </button>
                        )}

                        {scrollPosition < maxScroll && (
                            <button
                                className="absolute right-4 top-1/2 transform -translate-y-1/2 bg-gradient-to-r from-blue-600 to-purple-500 text-white p-3 rounded-full shadow-lg hover:scale-110 transition"
                                onClick={() => handleScroll('right')}
                            >
                                <svg
                                xmlns="http://www.w3.org/2000/svg"
                                className="h-6 w-6"
                                fill="none"
                                viewBox="0 0 24 24"
                                stroke="currentColor"
                            >
                                <path
                                    strokeLinecap="round"
                                    strokeLinejoin="round"
                                    strokeWidth={2}
                                    d="M9 5l7 7-7 7"
                                />
                            </svg>
                            </button>
                        )}
                    </section>

                    <section id="contact" className="contact-section bg-white shadow-lg rounded-lg p-8 my-12">
                        <AnimatedGradientText className="text-3xl font-bold text-center mb-6">
                            Contact Us
                        </AnimatedGradientText>
                        <p className="text-lg text-center mb-4">
                            Have questions? Reach out to us for more information about our AI solutions.
                        </p>
                        <div className="text-center">
                            <motion.a
                                className="text-blue-600 text-lg hover:underline"
                                href="mailto:contact@ai-insurance.com"
                                whileHover={{ color: "#6B46C1" }}
                            >
                                Email Us
                            </motion.a>
                        </div>
                    </section>

                    <section id="about-bottom" className="about-section bg-white shadow-lg rounded-lg p-8 my-12">
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
                    </section>
                </main>
            </div>
        </div>
    );
}

export default Home;

