
import { useGameContext } from "@/context/GameContext";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Button } from "@/components/ui/button";
import { ArrowUp, Coins, Map } from "lucide-react";
import UpgradesTab from "./tabs/UpgradesTab";
import LocationsTab from "./tabs/LocationsTab";

const BottomPanel = () => {
  const { gameState, toggleBottomPanel, setActiveTab } = useGameContext();
  const { isBottomPanelOpen, activeTab } = gameState;
  
  const handleTabChange = (value: string) => {
    setActiveTab(value as "upgrades" | "locations");
  };
  
  return (
    <div 
      className={`fixed bottom-0 inset-x-0 bg-card border-t border-border transition-transform duration-300 ease-in-out z-20 h-[65vh] ${
        isBottomPanelOpen ? "translate-y-0" : "translate-y-[calc(100%-3rem)]"
      }`}
    >
      <div 
        className="flex items-center justify-center h-12 cursor-pointer"
        onClick={toggleBottomPanel}
      >
        <Button variant="ghost" size="sm" className="gap-2">
          <ArrowUp className={`h-4 w-4 transition-transform ${isBottomPanelOpen ? "rotate-180" : ""}`} />
          {isBottomPanelOpen ? "Close" : "Open"} Panel
        </Button>
      </div>
      
      <div className="p-4 overflow-y-auto h-[calc(100%-3rem)]">
        <Tabs defaultValue={activeTab} onValueChange={handleTabChange} className="w-full">
          <TabsList className="grid grid-cols-2 mb-4">
            <TabsTrigger value="upgrades" className="flex items-center gap-2">
              <Coins className="w-4 h-4" />
              <span className="hidden sm:inline">Upgrades</span>
            </TabsTrigger>
            <TabsTrigger value="locations" className="flex items-center gap-2">
              <Map className="w-4 h-4" />
              <span className="hidden sm:inline">Locations</span>
            </TabsTrigger>
          </TabsList>
          
          <TabsContent value="upgrades" className="mt-0">
            <UpgradesTab />
          </TabsContent>
          
          <TabsContent value="locations" className="mt-0">
            <LocationsTab />
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
};

export default BottomPanel;
