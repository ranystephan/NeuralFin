import React, { useContext, useEffect } from 'react'
import Link from 'next/link'

const styles = {
  leftHeader: 'flex flex-1 text-white items-center gap-8 ml-5 mt-3 text-4xl',
  logo: 'object-cover cursor-pointer',
  rightHeader: 'flex items-center justify-end text-white gap-8 mr-5 mt-3 text-3xl',
  logoname: 'cursor-pointer font-bold hover:text-purple-700 duration-300 text-black',
  menuItem: 'cursor-pointer font-bold hover:text-purple-700 duration-300',
}

const Header_News = () => {
  return (
    <div className='page-container'>
      <div className='left-half'>
        <div className={styles.leftHeader}>
          {/* go to home page on click of neuralfin */}
          <Link href={"/"}>
            <div className={styles.logoname}>neuralfin</div>
          </Link>
        </div>
      </div>

      <div className='right-half'>
        <div className={styles.rightHeader}>
          <div className={styles.menuItem}>Portfolio Stock</div>
        </div>
      </div>
    </div>
  )
}

export default Header_News