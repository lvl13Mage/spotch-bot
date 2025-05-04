import React from 'react';
import type {ReactNode} from 'react';
import clsx from 'clsx';
import Heading from '@theme/Heading';
import Translate from '@docusaurus/Translate'; // Import the Translate component
import styles from './styles.module.css';

function FeatureSongRequests(): ReactNode {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center">
        <img
          src={require('@site/static/img/feature-song-request.png').default}
          alt="Song Requests"
          className={styles.featureImage}
          role="img"
        />
      </div>
      <div className="text--center padding-horiz--md">
        <Heading as="h3">
          <Translate id="landingPage.features.songRequests.title">
            Seamless Spotify Song Requests
          </Translate>
        </Heading>
        <p>
          <Translate id="landingPage.features.songRequests.description">
            Let your viewers request songs directly via channel points or chat commands. The bot integrates with Spotify’s API to add tracks to your playlist instantly — fully automated, flexible, and smooth.
          </Translate>
        </p>
      </div>
    </div>
  );
}

function FeatureModeration(): ReactNode {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center">
        <img
          src={require('@site/static/img/feature-moderation.png').default}
          alt="Moderation"
          className={styles.featureImage}
          role="img"
        />
      </div>
      <div className="text--center padding-horiz--md">
        <Heading as="h3">
          <Translate id="landingPage.features.moderation.title">
            Smart Moderation & Custom Controls
          </Translate>
        </Heading>
        <p>
          <Translate id="landingPage.features.moderation.description">
            Take full control over song requests with cooldowns, user limits, blacklists, manual approvals, and more. Designed to keep your stream’s vibe in check while staying viewer-friendly.
          </Translate>
        </p>
      </div>
    </div>
  );
}

function FeatureAPI(): ReactNode {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center">
        <img
          src={require('@site/static/img/feature-api.png').default}
          alt="API Integration"
          className={styles.featureImage}
          role="img"
        />
      </div>
      <div className="text--center padding-horiz--md">
        <Heading as="h3">
          <Translate id="landingPage.features.api.title">
            Powerful Stats & API Integrations
          </Translate>
        </Heading>
        <p>
          <Translate id="landingPage.features.api.description">
            Track who requested what and when, view song history, and search past requests. With a flexible API, the bot plays nicely with tools like Streamer.bot, allowing full integration into your stream setup.
          </Translate>
        </p>
      </div>
    </div>
  );
}

export default function HomepageFeatures(): ReactNode {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          <FeatureSongRequests />
          <FeatureModeration />
          <FeatureAPI />
        </div>
      </div>
    </section>
  );
}
