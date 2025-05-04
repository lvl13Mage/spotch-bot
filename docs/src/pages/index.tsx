import type {ReactNode} from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import HomepageFeatures from '@site/src/components/HomepageFeatures';
import Translate from '@docusaurus/Translate';
import {useColorMode} from '@docusaurus/theme-common'; // Import the useColorMode hook

import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  const {colorMode} = useColorMode(); // Get the current color mode

  // If colorMode is undefined, don't render the logo yet
  if (!colorMode) {
    return null;
  }

  // Choose the logo based on the color mode
  const logoSrc =
    colorMode === 'dark'
      ? require('@site/static/img/logo-transparent-purple-small.png').default
      : require('@site/static/img/logo-transparent-white-small.png').default;

  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <img
          src={logoSrc}
          alt="Spotch Bot Logo"
          className={clsx('hero__logo', styles.heroLogo)}
          role="img"
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
      title={`Hello from ${siteConfig.title}`}
      description="Description will go into a meta tag in <head />">
      <HomepageHeader />
      <main>
        <HomepageFeatures />
      </main>
    </Layout>
  );
}
