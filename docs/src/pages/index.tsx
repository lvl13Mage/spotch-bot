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
  const {colorMode} = useColorMode();

  // Ensure this component only renders on the client
  const isBrowser = typeof window !== 'undefined';

  if (!isBrowser) {
    // Avoid rendering during SSR
    return null;
  }

  const isDarkMode = colorMode === 'dark';

  const logoSrc = isDarkMode
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
      title={`${siteConfig.title} Documentation`}
      description="<Translate id='homepage.header.subtitle' />">
      <HomepageHeader />
      <main>
        <HomepageFeatures />
      </main>
    </Layout>
  );
}
