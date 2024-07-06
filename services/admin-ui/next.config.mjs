/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  output: "export",
  basePath: "/admin",
  distDir: 'dist',
  env: {
    ENVIRONMENT: process.env.ENVIRONMENT,
  },
};

export default nextConfig;
