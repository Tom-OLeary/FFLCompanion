import * as React from 'react';
import '../css/Temp.scss';

export default function Temp2() {

  return (
                  <div className="card" >
                      <section className="card-info card-section">
                          <i className="ion-navicon menu"></i>
                          <i className="ion-ios-search search"></i>

                          <div className="avatar row">
                          </div>

                          <section className="user row">
                              <h1 className="user-header">
                                  Bryan Smith
                                  {/*LEADER TEAM NAME*/}
                                  <h2 className="sub header">
                                      400 hours
                                  {/*    LEADER NAME*/}
                                  </h2>
                              </h1>
                          </section>

                          <section className="statistics">
                              <article className="statistic">
                                  <h4 className="statistic-title">
                                      Rank
                                  </h4>
                                  <h3 className="statistic-value">
                                      360
                                  </h3>
                              </article>

                              <article className="statistic">
                                  <h4 className="statistic-title">
                                      Score
                                  </h4>
                                  <h3 className="statistic-value">
                                      1,034
                                  </h3>
                              </article>
                          </section>

                          <div className="dial">
                              <h2 className="dial-title">
                                  35
                              </h2>
                              <h3 className="dial-value">
                                  Level
                              </h3>
                          </div>
                      </section>
                      <section className="card-details card-section">

                          <nav className="menu">
                              <article className="menu-item menu-item-active">
                                  Team
                              </article>
                              <article className="menu-item">
                                  Value
                              </article>
                          </nav>

                          <dl className="leaderboard">
                              <dt>
                                  <article className="progress">
                                      <section className="progress-bar" style={{width: "85%"}}></section>
                                  </article>
                              </dt>
                              <dd>
                                  <div className="leaderboard-name">Bryan Smith</div>
                                  <div className="leaderboard-value">20.123</div>
                              </dd>
                              <dt>
                                  <article className="progress">
                                      <section className="progress-bar" style={{width: "65%"}}></section>
                                  </article>
                              </dt>
                              <dd>
                                  <div className="leaderboard-name">Kevin Johnson</div>
                                  <div className="leaderboard-value">16.354</div>
                              </dd>
                              <dt>
                                  <article className="progress">
                                      <section className="progress-bar" style={{width: "60%"}}></section>
                                  </article>
                              </dt>
                              <dd>
                                  <div className="leaderboard-name">Glen Howie</div>
                                  <div className="leaderboard-value">15.873</div>
                              </dd>
                              <dt>
                                  <article className="progress">
                                      <section className="progress-bar" style={{width: "55%"}}></section>
                                  </article>
                              </dt>
                              <dd>
                                  <div className="leaderboard-name">Mark Desa</div>
                                  <div className="leaderboard-value">12.230</div>
                              </dd>
                              <dt>
                                  <article className="progress">
                                      <section className="progress-bar" style={{width: "35%"}}></section>
                                  </article>
                              </dt>
                              <dd>
                                  <div className="leaderboard-name">Martin Geiger</div>
                                  <div className="leaderboard-value">10.235</div>
                              </dd>
                              <dt>
                                  <article className="progress">
                                      <section className="progress-bar" style={{width: "35%"}}></section>
                                  </article>
                              </dt>
                              <dd>
                                  <div className="leaderboard-name">Martin Geiger</div>
                                  <div className="leaderboard-value">10.235</div>
                              </dd>
                              <dt>
                                  <article className="progress">
                                      <section className="progress-bar" style={{width: "35%"}}></section>
                                  </article>
                              </dt>
                              <dd>
                                  <div className="leaderboard-name">Martin Geiger</div>
                                  <div className="leaderboard-value">10.235</div>
                              </dd>
                              <dt>
                                  <article className="progress">
                                      <section className="progress-bar" style={{width: "35%"}}></section>
                                  </article>
                              </dt>
                              <dd>
                                  <div className="leaderboard-name">Martin Geiger</div>
                                  <div className="leaderboard-value">10.235</div>
                              </dd>
                          </dl>
                      </section>
                  </div>
  );
}
