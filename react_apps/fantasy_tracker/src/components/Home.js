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

function Home() {
    // let url = (env.NODE_ENV === 'production') ? 'https://www.troleary.com/api/' : 'http://127.0.0.1:8000/api/'
    // if (env.NODE_ENV === 'development') {
    //   url = 'http://127.0.0.1:8000/api/'
    // }
    // else if (env.NODE_ENV === 'production') {
    //   url = 'https://www.troleary.com/api/'
    // }
    // else {
    //   url = 'http://127.0.0.1:8000/api/'
    // }

  return (
    <>
        <Header />
        {/*<SpacingGrid />*/}
        {/*<GridTest url={url} />*/}
        {/*<DataGrid />*/}
        {/*<Sheet url={url} />*/}
        {/*<Footer />*/}
    </>
  );
}

export default Home;
