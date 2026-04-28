# Zomato AI Frontend

A modern Next.js frontend for Zomato AI that provides personalized restaurant recommendations based on user preferences.

## Features

- **Location-based restaurant discovery**
- **Budget filtering** with multiple price ranges
- **Rating slider** for minimum quality preferences
- **Cuisine selection** with visual cards
- **Responsive design** that works on all devices
- **Modern UI** with Tailwind CSS

## Getting Started

### Prerequisites

- Node.js 18+ installed
- npm or yarn package manager

### Installation

1. Install dependencies:
```bash
npm install
```

2. Run the development server:
```bash
npm run dev
```

3. Open [http://localhost:3000](http://localhost:3000) in your browser.

## Project Structure

```
├── app/
│   ├── globals.css      # Global styles
│   ├── layout.tsx       # Root layout component
│   └── page.tsx         # Main page component
├── components/          # Reusable components (if needed)
├── public/              # Static assets
├── tailwind.config.js   # Tailwind CSS configuration
├── tsconfig.json        # TypeScript configuration
└── package.json         # Dependencies and scripts
```

## Technologies Used

- **Next.js 14** - React framework with App Router
- **TypeScript** - Type-safe JavaScript
- **Tailwind CSS** - Utility-first CSS framework
- **Lucide React** - Icon library

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint

## Customization

The application is designed to be easily customizable:

- **Colors**: Modify `tailwind.config.js` to change the color scheme
- **Components**: Add new components in the `components/` directory
- **Styling**: Adjust Tailwind classes directly in components

## Future Enhancements

- Integration with Zomato API
- User authentication system
- Save preferences to database
- Advanced filtering options
- Restaurant detail pages
- Review and rating system
