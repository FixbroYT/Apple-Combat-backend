
import axios from 'axios';
import { GameState } from '@/types/game';

// Define the API base URL - replace with your actual FastAPI endpoint
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

// Create axios instance
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  }
});

// API functions
export const apiService = {
  // Save game state to server
  saveGameState: async (gameState: GameState): Promise<boolean> => {
    try {
      const response = await api.post('/save-game', gameState);
      return response.status === 200;
    } catch (error) {
      console.error('Error saving game state:', error);
      return false;
    }
  },

  // Load game state from server
  loadGameState: async (playerId: string): Promise<GameState | null> => {
    try {
      const response = await api.get(`/load-game/${playerId}`);
      return response.data;
    } catch (error) {
      console.error('Error loading game state:', error);
      return null;
    }
  },

  // Update player balance
  updateBalance: async (playerId: string, balance: number): Promise<boolean> => {
    try {
      const response = await api.post('/update-balance', { playerId, balance });
      return response.status === 200;
    } catch (error) {
      console.error('Error updating balance:', error);
      return false;
    }
  }
};
