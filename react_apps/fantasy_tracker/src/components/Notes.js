import * as React from 'react';
import HTMLFlipBook from "react-pageflip";
import '../css/Notes.css';

const Page = React.forwardRef((props, ref) => {
  return (
    <div className="demoPage" ref={ref}> /* ref required */
      <h1>Page Header</h1>
      <p>{props.children}</p>
      <p>Page number: {props.number}</p>
    </div>
  );
});

export default function Notes(props) {
  return (
      <div className="center-page">
          <HTMLFlipBook width={300} height={500} className="flip-book" >
              <Page number="1">Page text</Page>
              <Page number="2">Page text</Page>
              <Page number="3">Page text</Page>
              <Page number="4">Page text</Page>
          </HTMLFlipBook>
      </div>
  );
}