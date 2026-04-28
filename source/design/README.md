# Zomato AI - Preference Hub UI

A modern, responsive frontend for the Zomato AI restaurant recommendation system, built with Next.js and Tailwind CSS.

## Features

- **Modern UI Design**: Clean, intuitive interface matching the Zomato AI brand
- **Interactive Components**: Location input, budget selection, rating slider, cuisine preferences
- **Responsive Design**: Optimized for desktop, tablet, and mobile devices
- **Smooth Animations**: Hover effects and transitions for enhanced user experience
- **TypeScript**: Full TypeScript support for type safety

## Design Elements

### Header
- Zomato AI branding
- Navigation menu (Preference Hub, Trending, Saved, History)
- Sign In button

### Hero Section
- "Your Personalized Food Journey" title
- Descriptive subtitle about AI-powered recommendations

### Input Cards
- **Location Card**: Input field with detect button
- **Budget Card**: Four budget options ($15, $30, $50, $100+)
- **Rating Card**: Interactive slider (3.0-5.0) with star display
- **Cuisines Card**: Grid of cuisine options with images

### Call to Action
- Prominent "Find my next meal" button
- Informative subtitle about AI suggestions

### Footer
- Zomato AI branding
- Legal links (Privacy Policy, Terms of Service, AI Methodology, Feedback)
- Copyright information

## Color Scheme

- **Primary**: Red (#ef4444) - Matching Zomato brand
- **Secondary**: Gray tones for backgrounds and borders
- **Accent**: White for cards and inputs

## Technologies Used

- **Next.js 14**: React framework with App Router
- **TypeScript**: Type-safe JavaScript
- **Tailwind CSS**: Utility-first CSS framework
- **Lucide React**: Modern icon library

## Getting Started

1. Install dependencies:
   ```bash
   npm install
   ```

2. Run the development server:
   ```bash
   npm run dev
   ```

3. Open [http://localhost:3000](http://localhost:3000) in your browser

## Project Structure

```
design/
├── page.tsx          # Main page component
├── layout.tsx        # Root layout
├── globals.css       # Global styles
├── tailwind.config.js # Tailwind configuration
├── tsconfig.json     # TypeScript configuration
├── package.json      # Dependencies and scripts
└── README.md         # This file
```

## Custom Components

### BudgetButton
Interactive budget selection with active state styling and hover effects.

### CuisineCard
Clickable cuisine cards with image placeholders and selection states.

### RatingSlider
Custom-styled range input for minimum rating selection.

### LocationInput
Location input field with detect functionality placeholder.

## Responsive Design

- **Desktop**: Full grid layout with all components visible
- **Tablet**: Adjusted spacing and sizing
- **Mobile**: Stacked layout with optimized touch targets

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

© 2024 Zomato AI Recommendation Engine. All rights reserved.
