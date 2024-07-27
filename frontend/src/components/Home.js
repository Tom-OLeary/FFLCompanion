// import './App.css';
import Header from "./home/Header";
// import Sheet from "./components/Sheet";
// import DataGrid from "./components/DataGrid";
import env from "react-dotenv";
// import GridTest from "./components/GridTest";
// import TeamCard from "./components/TeamCard";
// import SpacingGrid from "./components/SpacingGrid";
// import MenuDrawer from "./components/MenuDrawer";
import React from "react";

function Home(props) {

  return (
    <>
        <Header url={props.url}/>
        {/*<SpacingGrid />*/}
        {/*<GridTest url={url} />*/}
        {/*<DataGrid />*/}
        {/*<Sheet url={url} />*/}
        {/*<Footer />*/}
    </>
  );
}

export default Home;
