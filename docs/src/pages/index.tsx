import type {ReactNode} from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import HomepageFeatures from '@site/src/components/HomepageFeatures';
import Translate from '@docusaurus/Translate';
import {useColorMode} from '@docusaurus/theme-common';
import ThemedImage from '@theme/ThemedImage'; // Import ThemedImage component

import styles from './index.module.css';

function HomepageHeader() {
  const logoSources = {
    light: require('@site/static/img/logo-transparent-white-small.png').default,
    dark: require('@site/static/img/logo-transparent-purple-small.png').default,
  };

  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <ThemedImage
          sources={logoSources}
          alt="Spotch Bot Logo"
          className={clsx('hero__logo', styles.heroLogo)}
          style={{
            height: '300px',
            borderRadius: '15px',
          }}
        />
        <p className="hero__subtitle">
          <Translate id="homepage.header.subtitle" />
        </p>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/docs/intro">
            <Translate id="homepage.header.buttonText" />
          </Link>
        </div>
      </div>
    </header>
  );
}

export default function Home(): ReactNode {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`${siteConfig.title} Documentation`}
      description="<Translate id='homepage.header.subtitle' />">
      <HomepageHeader />
      <main>
        <HomepageFeatures />
      </main>
    </Layout>
  );
}
