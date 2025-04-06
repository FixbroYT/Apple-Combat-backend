
export interface Player {
  id: string;
  name: string;
  balance: number;
  totalEarned: number;
  clickPower: number;
  unlockedLocations: string[];
  currentLocation: string;
}

export interface Upgrade {
  id: string;
  name: string;
  description: string;
  baseCost: number;
  currentLevel: number;
  coinMultiplier: number;
  icon: string;
}

export interface Location {
  id: string;
  name: string;
  description: string;
  unlockCost: number;
  coinMultiplier: number;
  background: string;
  isUnlocked: boolean;
}

export interface GameState {
  player: Player;
  upgrades: Upgrade[];
  locations: Location[];
  isBottomPanelOpen: boolean;
  activeTab: "upgrades" | "locations";
}
