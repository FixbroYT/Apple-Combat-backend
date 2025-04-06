
import React, { createContext, useContext, useState, useEffect, ReactNode } from "react";
import { GameState, Upgrade, Location, Player } from "@/types/game";
import { Coins, Map } from "lucide-react";
import { useToast } from "@/hooks/use-toast";

// Initial game state
const initialPlayer: Player = {
  id: "player1",
  name: "Player",
  balance: 0,
  totalEarned: 0,
  clickPower: 1,
  unlockedLocations: ["home"],
  currentLocation: "home"
};

const initialUpgrades: Upgrade[] = [
  {
    id: "click-power",
    name: "Click Power",
    description: "Increase coins per click",
    baseCost: 10,
    currentLevel: 0,
    coinMultiplier: 1,
    icon: "zap"
  },
  {
    id: "auto-clicker",
    name: "Auto Clicker",
    description: "Automatically clicks for you",
    baseCost: 50,
    currentLevel: 0,
    coinMultiplier: 0.2,
    icon: "mouse-pointer-click"
  }
];

const initialLocations: Location[] = [
  {
    id: "home",
    name: "Home",
    description: "Your starting location",
    unlockCost: 0,
    coinMultiplier: 1,
    background: "bg-gradient-to-br from-blue-100 to-blue-200",
    isUnlocked: true
  },
  {
    id: "garden",
    name: "Garden",
    description: "A peaceful garden with more coins",
    unlockCost: 100,
    coinMultiplier: 1.5,
    background: "bg-gradient-to-br from-green-100 to-green-300",
    isUnlocked: false
  },
  {
    id: "mine",
    name: "Gold Mine",
    description: "Rich in resources",
    unlockCost: 500,
    coinMultiplier: 2,
    background: "bg-gradient-to-br from-amber-100 to-amber-300",
    isUnlocked: false
  }
];

const initialGameState: GameState = {
  player: initialPlayer,
  upgrades: initialUpgrades,
  locations: initialLocations,
  isBottomPanelOpen: false,
  activeTab: "upgrades"
};

interface GameContextProps {
  gameState: GameState;
  addCoins: (amount: number) => void;
  purchaseUpgrade: (upgradeId: string) => void;
  unlockLocation: (locationId: string) => void;
  setCurrentLocation: (locationId: string) => void;
  toggleBottomPanel: () => void;
  setActiveTab: (tab: "upgrades" | "locations") => void;
}

const GameContext = createContext<GameContextProps | undefined>(undefined);

export const GameProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [gameState, setGameState] = useState<GameState>(initialGameState);
  const { toast } = useToast();
  
  // Auto-save game state to localStorage
  useEffect(() => {
    const savedState = localStorage.getItem("coinQuestGameState");
    if (savedState) {
      try {
        setGameState(JSON.parse(savedState));
      } catch (error) {
        console.error("Failed to load saved game state:", error);
      }
    }
  }, []);

  // Save game state to localStorage whenever it changes
  useEffect(() => {
    localStorage.setItem("coinQuestGameState", JSON.stringify(gameState));
  }, [gameState]);

  // Auto-clicker effect
  useEffect(() => {
    const autoClickerUpgrade = gameState.upgrades.find(u => u.id === "auto-clicker");
    if (autoClickerUpgrade && autoClickerUpgrade.currentLevel > 0) {
      const coinsPerSecond = autoClickerUpgrade.currentLevel * autoClickerUpgrade.coinMultiplier;
      const interval = setInterval(() => {
        addCoins(coinsPerSecond);
      }, 1000);
      
      return () => clearInterval(interval);
    }
  }, [gameState.upgrades]);

  const addCoins = (amount: number) => {
    const currentLocation = gameState.locations.find(
      l => l.id === gameState.player.currentLocation
    );
    
    const locationMultiplier = currentLocation ? currentLocation.coinMultiplier : 1;
    const actualAmount = amount * locationMultiplier;
    
    setGameState(prevState => ({
      ...prevState,
      player: {
        ...prevState.player,
        balance: prevState.player.balance + actualAmount,
        totalEarned: prevState.player.totalEarned + actualAmount
      }
    }));
  };

  const purchaseUpgrade = (upgradeId: string) => {
    const upgradeIndex = gameState.upgrades.findIndex(u => u.id === upgradeId);
    if (upgradeIndex === -1) return;

    const upgrade = gameState.upgrades[upgradeIndex];
    const cost = upgrade.baseCost * Math.pow(1.5, upgrade.currentLevel);

    if (gameState.player.balance >= cost) {
      // Update player balance
      const newBalance = gameState.player.balance - cost;
      
      // Update upgrade level
      const newUpgrades = [...gameState.upgrades];
      newUpgrades[upgradeIndex] = {
        ...upgrade,
        currentLevel: upgrade.currentLevel + 1
      };

      // Update click power if it's the click power upgrade
      let newClickPower = gameState.player.clickPower;
      if (upgradeId === "click-power") {
        newClickPower += 1;
      }

      setGameState(prevState => ({
        ...prevState,
        player: {
          ...prevState.player,
          balance: newBalance,
          clickPower: newClickPower
        },
        upgrades: newUpgrades
      }));

      toast({
        title: "Upgrade Purchased!",
        description: `You've upgraded ${upgrade.name} to level ${upgrade.currentLevel + 1}.`
      });
    } else {
      toast({
        title: "Not enough coins",
        description: `You need ${cost} coins to purchase this upgrade.`,
        variant: "destructive"
      });
    }
  };

  const unlockLocation = (locationId: string) => {
    const locationIndex = gameState.locations.findIndex(l => l.id === locationId);
    if (locationIndex === -1) return;

    const location = gameState.locations[locationIndex];
    
    if (gameState.player.balance >= location.unlockCost && !location.isUnlocked) {
      const newBalance = gameState.player.balance - location.unlockCost;
      
      const newLocations = [...gameState.locations];
      newLocations[locationIndex] = {
        ...location,
        isUnlocked: true
      };

      const newUnlockedLocations = [...gameState.player.unlockedLocations, locationId];

      setGameState(prevState => ({
        ...prevState,
        player: {
          ...prevState.player,
          balance: newBalance,
          unlockedLocations: newUnlockedLocations,
          currentLocation: locationId
        },
        locations: newLocations
      }));

      toast({
        title: "New Location Unlocked!",
        description: `You've unlocked ${location.name}. Enjoy the new scenery!`
      });
    } else if (location.isUnlocked) {
      setCurrentLocation(locationId);
    } else {
      toast({
        title: "Not enough coins",
        description: `You need ${location.unlockCost} coins to unlock this location.`,
        variant: "destructive"
      });
    }
  };

  const setCurrentLocation = (locationId: string) => {
    if (gameState.player.unlockedLocations.includes(locationId)) {
      setGameState(prevState => ({
        ...prevState,
        player: {
          ...prevState.player,
          currentLocation: locationId
        }
      }));
    }
  };

  const toggleBottomPanel = () => {
    setGameState(prevState => ({
      ...prevState,
      isBottomPanelOpen: !prevState.isBottomPanelOpen
    }));
  };

  const setActiveTab = (tab: "upgrades" | "locations") => {
    setGameState(prevState => ({
      ...prevState,
      activeTab: tab
    }));
  };

  return (
    <GameContext.Provider
      value={{
        gameState,
        addCoins,
        purchaseUpgrade,
        unlockLocation,
        setCurrentLocation,
        toggleBottomPanel,
        setActiveTab
      }}
    >
      {children}
    </GameContext.Provider>
  );
};

export const useGameContext = () => {
  const context = useContext(GameContext);
  if (context === undefined) {
    throw new Error("useGameContext must be used within a GameProvider");
  }
  return context;
};
