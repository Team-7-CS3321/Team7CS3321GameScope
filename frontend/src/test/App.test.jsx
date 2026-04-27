import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import App from '../App'


beforeEach(() => {
  // Default mock returns empty results for any unmocked fetch calls
  // (e.g. the recommendations fetch that follows the main /report/ fetch)
  global.fetch = vi.fn().mockResolvedValue({
    json: async () => ({ results: [] }),
  })
})


describe('getDifficultyLabel', () => {
  it('shows Very Easy for score <= 20', async () => {
    global.fetch.mockResolvedValueOnce({
      json: async () => ({
        data: {
          game: {
            name: 'Test Game',
            release_date: '2022-01-01',
            rating: 4.5,
            genres: ['RPG'],
            achievement_count: 10,
            description: 'A test game',
            difficulty_score: 10,
            achievements: [],
          },
        },
      }),
    })
    render(<App />)
    fireEvent.click(screen.getByText('Search'))
    await screen.findByText(/Very Easy/i)
    expect(screen.getByText(/Very Easy/i)).toBeInTheDocument()
  })

  it('shows Easy for score <= 40', async () => {
    global.fetch.mockResolvedValueOnce({
      json: async () => ({
        data: {
          game: {
            name: 'Test Game',
            release_date: '2022-01-01',
            rating: 4.5,
            genres: ['RPG'],
            achievement_count: 10,
            description: 'A test game',
            difficulty_score: 30,
            achievements: [],
          },
        },
      }),
    })
    render(<App />)
    fireEvent.click(screen.getByText('Search'))
    await screen.findByText(/Easy/i)
    expect(screen.getByText(/Easy/i)).toBeInTheDocument()
  })

  it('shows Moderate for score <= 60', async () => {
    global.fetch.mockResolvedValueOnce({
      json: async () => ({
        data: {
          game: {
            name: 'Test Game',
            release_date: '2022-01-01',
            rating: 4.5,
            genres: ['RPG'],
            achievement_count: 10,
            description: 'A test game',
            difficulty_score: 50,
            achievements: [],
          },
        },
      }),
    })
    render(<App />)
    fireEvent.click(screen.getByText('Search'))
    await screen.findByText(/Moderate/i)
    expect(screen.getByText(/Moderate/i)).toBeInTheDocument()
  })

  it('shows Hard for score <= 80', async () => {
    global.fetch.mockResolvedValueOnce({
      json: async () => ({
        data: {
          game: {
            name: 'Test Game',
            release_date: '2022-01-01',
            rating: 4.5,
            genres: ['RPG'],
            achievement_count: 10,
            description: 'A test game',
            difficulty_score: 70,
            achievements: [],
          },
        },
      }),
    })
    render(<App />)
    fireEvent.click(screen.getByText('Search'))
    await screen.findByText(/Hard\b/i)
    expect(screen.getByText(/Hard\b/i)).toBeInTheDocument()
  })

  it('shows Very Hard for score > 80', async () => {
    global.fetch.mockResolvedValueOnce({
      json: async () => ({
        data: {
          game: {
            name: 'Test Game',
            release_date: '2022-01-01',
            rating: 4.5,
            genres: ['RPG'],
            achievement_count: 10,
            description: 'A test game',
            difficulty_score: 90,
            achievements: [],
          },
        },
      }),
    })
    render(<App />)
    fireEvent.click(screen.getByText('Search'))
    await screen.findByText(/Very Hard/i)
    expect(screen.getByText(/Very Hard/i)).toBeInTheDocument()
  })
})

describe('App component', () => {
  it('renders without crashing', () => {
    render(<App />)
    expect(screen.getByPlaceholderText(/search for a game/i)).toBeInTheDocument()
  })

  it('renders search button', () => {
    render(<App />)
    expect(screen.getByText('Search')).toBeInTheDocument()
  })

  it('renders logo image', () => {
    render(<App />)
    expect(screen.getByAltText('GameScope Logo')).toBeInTheDocument()
  })

  it('does not show results before searching', () => {
    render(<App />)
    expect(screen.queryByText(/Release Date/i)).not.toBeInTheDocument()
  })

  it('shows game data after successful search', async () => {
    global.fetch.mockResolvedValueOnce({
      json: async () => ({
        data: {
          game: {
            name: 'Elden Ring',
            release_date: '2022-02-25',
            rating: 4.5,
            genres: ['RPG'],
            achievement_count: 42,
            description: 'An action RPG.',
            difficulty_score: 75,
            achievements: [],
          },
        },
      }),
    })
    render(<App />)
    fireEvent.click(screen.getByText('Search'))
    await screen.findByText('Elden Ring')
    expect(screen.getByText('Elden Ring')).toBeInTheDocument()
    expect(screen.getByText(/Release Date/i)).toBeInTheDocument()
  })

  it('handles fetch error gracefully without crashing', async () => {
    global.fetch.mockRejectedValueOnce(new Error('Network error'))
    render(<App />)
    fireEvent.click(screen.getByText('Search'))
    await new Promise((r) => setTimeout(r, 100))
    expect(screen.getByPlaceholderText(/search for a game/i)).toBeInTheDocument()
  })
})

  it('shows loading spinner when searching', async () => {
    global.fetch = vi.fn(() => new Promise(() => {}))
    render(<App />)
    fireEvent.click(screen.getByText('Search'))
    expect(document.querySelector('.loader')).toBeInTheDocument()
  })

  it('shows no results message when game not found', async () => {
    global.fetch.mockResolvedValueOnce({
      json: async () => ({ data: null })
    })
    render(<App />)
    fireEvent.click(screen.getByText('Search'))
    await screen.findByText('No results found')
    expect(screen.getByText('Try a different game name.')).toBeInTheDocument()
  })

  it('shows no achievements message when achievements empty', async () => {
    global.fetch
      .mockResolvedValueOnce({
        json: async () => ({
          data: {
            game: {
              name: 'Test Game',
              release_date: '2022-01-01',
              rating: 4.5,
              genres: ['RPG'],
              achievement_count: 0,
              description: 'A test game',
              difficulty_score: 0,
              achievements: [],
              cover_art: null,
            },
          },
        }),
      })
      .mockResolvedValueOnce({
        json: async () => ({ results: [] }),
      })
    render(<App />)
    fireEvent.click(screen.getByText('Search'))
    await screen.findByText('Test Game')
    expect(screen.getByText('No achievements → difficulty not available.')).toBeInTheDocument()
  })

  it('shows recommendations when available', async () => {
    global.fetch
      .mockResolvedValueOnce({
        json: async () => ({
          data: {
            game: {
              name: 'Elden Ring',
              release_date: '2022-02-25',
              rating: 4.5,
              genres: ['RPG'],
              achievement_count: 42,
              description: 'An action RPG.',
              difficulty_score: 75,
              achievements: [],
              cover_art: null,
            },
          },
        }),
      })
      .mockResolvedValueOnce({
        json: async () => ({
          results: [
            { name: 'Dark Souls', cover_art: null },
            { name: 'Bloodborne', cover_art: null },
          ],
        }),
      })
    render(<App />)
    fireEvent.click(screen.getByText('Search'))
    await screen.findByText('Elden Ring')
    expect(screen.getByText('Dark Souls')).toBeInTheDocument()
    expect(screen.getByText('Bloodborne')).toBeInTheDocument()
  })

  it('shows no recommendations message when none available', async () => {
    global.fetch
      .mockResolvedValueOnce({
        json: async () => ({
          data: {
            game: {
              name: 'Test Game',
              release_date: '2022-01-01',
              rating: 4.5,
              genres: ['RPG'],
              achievement_count: 10,
              description: 'A test game',
              difficulty_score: 50,
              achievements: [],
              cover_art: null,
            },
          },
        }),
      })
      .mockResolvedValueOnce({
        json: async () => ({ results: [] }),
      })
    render(<App />)
    fireEvent.click(screen.getByText('Search'))
    await screen.findByText('Test Game')
    expect(screen.getByText('No recommendations available.')).toBeInTheDocument()
  })

  it('shows achievement popup when achievement clicked', async () => {
    global.fetch
      .mockResolvedValueOnce({
        json: async () => ({
          data: {
            game: {
              name: 'Elden Ring',
              release_date: '2022-02-25',
              rating: 4.5,
              genres: ['RPG'],
              achievement_count: 1,
              description: 'An action RPG.',
              difficulty_score: 75,
              achievements: [
                {
                  display_name: 'First Kill',
                  global_percentage: 21.5,
                  icon: '',
                  description: 'Kill your first enemy',
                },
              ],
              cover_art: null,
            },
          },
        }),
      })
      .mockResolvedValueOnce({
        json: async () => ({ results: [] }),
      })
    render(<App />)
    fireEvent.click(screen.getByText('Search'))
    await screen.findByText('Elden Ring')
    fireEvent.click(screen.getAllByText(/First Kill/)[0])
    expect(screen.getByText('Kill your first enemy')).toBeInTheDocument()
    expect(screen.getByText('Global Completion:')).toBeInTheDocument()
  })
