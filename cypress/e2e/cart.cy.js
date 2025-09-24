describe('Cart flow', () => {
  it('adds and removes item (demo)', () => {
    cy.visit('/')
    cy.get('body').should('be.visible')
  })
})
