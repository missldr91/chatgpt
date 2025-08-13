export interface Lesson {
  id: string;
  title: string;
  slides: number;
  students: number;
  created: string;
  status: 'draft' | 'published';
}

export const lessons: Lesson[] = [
  {
    id: 'ml-intro',
    title: 'Introduction to Machine Learning',
    slides: 12,
    students: 45,
    created: '2024-01-15',
    status: 'published',
  },
  {
    id: 'ds-algo',
    title: 'Data Structures & Algorithms',
    slides: 18,
    students: 32,
    created: '2024-02-10',
    status: 'published',
  },
  {
    id: 'digital-marketing',
    title: 'Digital Marketing Fundamentals',
    slides: 15,
    students: 28,
    created: '2024-03-05',
    status: 'draft',
  },
];
