/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  async rewrites() {
    return [
      {
        source: '/api/scan',
        destination: process.env.NEXT_PUBLIC_BACKEND_URL + '/scan',
      },
      {
        source: '/api/scan/:id',
        destination: process.env.NEXT_PUBLIC_BACKEND_URL + '/scan/:id',
      },
    ];
  },
};

module.exports = nextConfig;
