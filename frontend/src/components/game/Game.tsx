
import { useEffect } from "react";
import { useGameContext } from "@/context/GameContext";
import CoinButton from "./CoinButton";
import GameHeader from "./GameHeader";
import BottomPanel from "./BottomPanel";

declare global {
  interface Window {
    Telegram?: {
      WebApp: {
        ready: () => void;
        expand: () => void;
        close: () => void;
        MainButton: {
          show: () => void;
          hide: () => void;
          setText: (text: string) => void;
          onClick: (callback: () => void) => void;
        };
      };
    };
  }
}

const Game = () => {
  const { gameState } = useGameContext();
  const currentLocation = gameState.locations.find(
    location => location.id === gameState.player.currentLocation
  );
  
  // Detect if we're running in Telegram WebApp
  useEffect(() => {
    // Check if Telegram WebApp is available
    if (window.Telegram?.WebApp) {
      const tg = window.Telegram.WebApp;
      // Init Telegram WebApp
      tg.expand();
      tg.ready();
      
      console.log("Telegram WebApp initialized");
    } else {
      console.log("Running outside of Telegram WebApp");
    }
  }, []);
  
  return (
    <main className={`min-h-screen pt-16 pb-20 ${currentLocation?.background || "bg-background"}`}>
      <GameHeader />
      
      <div className="flex flex-col items-center justify-center h-[calc(100vh-12rem)]">
        <CoinButton />
      </div>
      
      <BottomPanel />
    </main>
  );
};

export default Game;
